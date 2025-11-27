import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
import { ToastController } from '@ionic/angular/standalone';

// Imports Visuais
import { 
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton,
  IonItem, IonLabel, IonInput, IonSelect, IonSelectOption, IonTextarea, IonButton,
  IonIcon 
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { cloudUploadOutline, checkmarkCircle } from 'ionicons/icons';

@Component({
  selector: 'app-anunciar',
  templateUrl: './anunciar.page.html',
  styleUrls: ['./anunciar.page.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule, 
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, 
    IonItem, IonLabel, IonInput, IonSelect, IonSelectOption, IonTextarea, IonButton,
    IonIcon
  ]
})
export class AnunciarPage {
  
  prod = { nome: '', preco: '', estoque: 1, plataforma: '', categoria: '', descricao: '' };
  
  arquivoImagem: File | null = null;

  constructor(
    private api: ApiService, 
    private router: Router,
    private toast: ToastController
  ) {
    addIcons({ cloudUploadOutline, checkmarkCircle });
  }

  selecionarImagem(event: any) {
    if (event.target.files && event.target.files[0]) {
      this.arquivoImagem = event.target.files[0];
    }
  }

  salvar() {
    // Validação básica
    if (!this.prod.nome || !this.prod.preco) {
      this.mostrarToast('Preencha pelo menos Nome e Preço!', 'warning');
      return;
    }

    const formData = new FormData();
    formData.append('nome', this.prod.nome);
    // Converte preço para string e troca vírgula por ponto
    formData.append('preco', String(this.prod.preco).replace(',', '.'));
    
 
    formData.append('estoque', String(this.prod.estoque));

    formData.append('plataforma', this.prod.plataforma || 'OUTRO');
    formData.append('categoria', this.prod.categoria || 'JOGO');
    formData.append('descricao', this.prod.descricao || '');
    
    if (this.arquivoImagem) {
      formData.append('imagem', this.arquivoImagem);
    }

    this.api.criarProduto(formData).subscribe({
      next: async () => {
        this.mostrarToast('Anúncio criado com sucesso!', 'success');
        this.router.navigate(['/home']);
      },
      error: async (err) => {
        console.error('Erro detalhado:', err);
        let msg = 'Erro ao criar anúncio.';
        
        if (err.error) {
            
            if (typeof err.error === 'object') {
                msg = Object.values(err.error).join(' ');
            } else {
                msg = err.error.toString();
            }
        }
        this.mostrarToast(msg, 'danger');
      }
    });
  }

  async mostrarToast(msg: string, cor: string) {
    const t = await this.toast.create({ message: msg, duration: 3000, color: cor, position: 'bottom' });
    t.present();
  }
}