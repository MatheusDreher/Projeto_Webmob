import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api.service';
import { RouterLink } from '@angular/router'; // <--- Importante para o botão funcionar
import { 
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton,
  IonList, IonItem, IonLabel, IonThumbnail, IonButton, IonIcon,
  AlertController, ToastController
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { trashOutline, createOutline } from 'ionicons/icons'; // <--- Importados juntos

@Component({
  selector: 'app-meus-anuncios',
  templateUrl: './meus-anuncios.page.html',
  styleUrls: ['./meus-anuncios.page.scss'],
  standalone: true,
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton,
    IonList, IonItem, IonLabel, IonThumbnail, IonButton, IonIcon,
    CommonModule,
    RouterLink // <--- Adicionado na lista de imports
  ]
})
export class MeusAnunciosPage {
  itens: any[] = [];

  constructor(
    private api: ApiService,
    private alertCtrl: AlertController,
    private toastCtrl: ToastController
  ) {
    // Registra o Lixo e o Lápis
    addIcons({ trashOutline, createOutline }); 
  }

  ionViewWillEnter() {
    this.carregar();
  }

  carregar() {
    this.api.getMeusAnuncios().subscribe({
      next: (res: any) => this.itens = res,
      error: (err: any) => console.error(err)
    });
  }

  async confirmarExclusao(produto: any) {
    const alert = await this.alertCtrl.create({
      header: 'Apagar Anúncio?',
      message: `Tem certeza que deseja apagar "${produto.nome}"?`,
      buttons: [
        { text: 'Cancelar', role: 'cancel' },
        { 
          text: 'Apagar', 
          role: 'destructive',
          handler: () => this.deletar(produto.id)
        }
      ]
    });
    await alert.present();
  }

  deletar(id: any) {
    this.api.deletarProduto(id).subscribe({
      next: async () => {
        this.carregar(); 
        const t = await this.toastCtrl.create({ message: 'Anúncio removido!', duration: 2000 });
        t.present();
      },
      error: (err) => console.error(err)
    });
  }
}