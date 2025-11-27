import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router'; // Importando Router para navegação via código
import { CarrinhoService } from '../services/carrinho.service';
import { ApiService } from '../services/api.service'; // Importando API para baixar estoque

// Imports dos Componentes Visuais e Controller de Toast
import { 
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton,
  IonList, IonItem, IonLabel, IonThumbnail, IonButton, IonFooter,
  IonIcon, ToastController
} from '@ionic/angular/standalone';

// Imports de Ícones
import { addIcons } from 'ionicons';
import { trashOutline, cartOutline } from 'ionicons/icons';

@Component({
  selector: 'app-carrinho',
  templateUrl: './carrinho.page.html',
  styleUrls: ['./carrinho.page.scss'],
  standalone: true,
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton,
    IonList, IonItem, IonLabel, IonThumbnail, IonButton, IonFooter,
    IonIcon,
    CommonModule, RouterLink
  ]
})
export class CarrinhoPage {
  itens: any[] = [];
  total: number = 0;

  constructor(
    private carrinhoService: CarrinhoService,
    private apiService: ApiService,     // <--- Para falar com o Django
    private router: Router,             // <--- Para navegar após compra
    private toastCtrl: ToastController  // <--- Para mostrar mensagem
  ) {
    // Registrando ícones usados no HTML
    addIcons({ trashOutline, cartOutline });
  }

  // Executa toda vez que a tela vai aparecer (atualiza dados)
  ionViewWillEnter() {
    this.carregarCarrinho();
  }

  carregarCarrinho() {
    this.itens = this.carrinhoService.getItens();
    this.total = this.carrinhoService.getTotal();
  }

  removerItem(index: number) {
    this.carrinhoService.removerItem(index);
    this.carregarCarrinho(); // Recalcula o total e atualiza a lista
  }
  
  // Função que finaliza a compra e baixa o estoque
  finalizarCompra() {
    if (this.itens.length === 0) return;

    // 1. Cria uma lista apenas com os IDs dos produtos para mandar pro backend
    const ids = this.itens.map(item => item.id);

    // 2. Chama a API do Django
    this.apiService.realizarCompra(ids).subscribe({
      next: async () => {
        // SUCESSO!
        this.carrinhoService.limparCarrinho(); // Esvazia a memória do celular
        this.carregarCarrinho(); // Atualiza a tela (vai ficar vazia)
        
        // Mostra mensagem verde
        const t = await this.toastCtrl.create({ 
          message: 'Compra realizada com sucesso! 🎉', 
          duration: 3000, 
          color: 'success',
          position: 'middle'
        });
        t.present();

        // Volta para a loja
        this.router.navigate(['/home']); 
      },
      error: async (err) => {
        // ERRO
        console.error(err);
        const t = await this.toastCtrl.create({ 
          message: 'Erro ao processar compra. Tente novamente.', 
          duration: 2000, 
          color: 'danger' 
        });
        t.present();
      }
    });
  }
}