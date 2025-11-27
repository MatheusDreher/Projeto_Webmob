import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastController } from '@ionic/angular/standalone';

// Imports Visuais
import { 
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton,
  IonItem, IonLabel, IonInput, IonSelect, IonSelectOption, IonTextarea, IonButton,
  IonIcon
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { checkmarkCircle } from 'ionicons/icons';

@Component({
  selector: 'app-editar-anuncio',
  templateUrl: './editar-anuncio.page.html',
  styleUrls: ['./editar-anuncio.page.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule, 
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, 
    IonItem, IonLabel, IonInput, IonSelect, IonSelectOption, IonTextarea, IonButton,
    IonIcon
  ]
})
export class EditarAnuncioPage implements OnInit {
  prod: any = { nome: '', preco: '', plataforma: '', categoria: '', descricao: '', imagem: '' };
  arquivoImagem: File | null = null;
  idProduto: any;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private toast: ToastController
  ) { 
    addIcons({ checkmarkCircle });
  }

  ngOnInit() {
    this.idProduto = this.route.snapshot.paramMap.get('id');
    this.carregarDados();
  }

  carregarDados() {
    this.api.getProduto(this.idProduto).subscribe({
      next: (res: any) => {
        this.prod = res;
      },
      error: (err) => {
        this.mostrarToast('Erro ao carregar dados', 'danger');
        this.router.navigate(['/meus-anuncios']);
      }
    });
  }

  selecionarImagem(event: any) {
    if (event.target.files && event.target.files[0]) {
      this.arquivoImagem = event.target.files[0];
    }
  }

  salvar() {
    const formData = new FormData();
    
    // 1. Adiciona os campos de texto
    formData.append('nome', this.prod.nome);
    formData.append('plataforma', this.prod.plataforma);
    formData.append('categoria', this.prod.categoria);
    formData.append('descricao', this.prod.descricao || ''); // Garante que não vá 'undefined'
    formData.append('estoque', this.prod.estoque);

    // 2. CORREÇÃO DE PREÇO: Garante que usa PONTO em vez de VÍRGULA
    let precoString = String(this.prod.preco).replace(',', '.');
    formData.append('preco', precoString);
    
    // 3. Só envia imagem se o usuário tiver escolhido uma NOVA
    if (this.arquivoImagem) {
      formData.append('imagem', this.arquivoImagem);
    }

    this.api.atualizarProduto(this.idProduto, formData).subscribe({
      next: async () => {
        this.mostrarToast('Anúncio atualizado com sucesso!', 'success');
        this.router.navigate(['/meus-anuncios']);
      },
      error: async (err) => {
        console.error(err); // Veja o erro detalhado no Console (F12)
        
        // Tenta mostrar o erro específico do Django na tela
        let mensagemErro = 'Erro ao salvar.';
        if (err.status === 400) {
           mensagemErro = 'Verifique os dados (Preço ou Campos obrigatórios).';
        }
        
        this.mostrarToast(mensagemErro, 'danger');
      }
    });
  }

  async mostrarToast(msg: string, cor: string) {
    const t = await this.toast.create({ message: msg, duration: 3000, color: cor, position: 'bottom' });
    t.present();
  }
}