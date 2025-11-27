import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../services/api.service';
import { CarrinhoService } from '../services/carrinho.service';
import { 
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, 
  IonChip, IonLabel, IonSpinner, IonButton, ToastController,
  IonFooter // <--- 1. Importado aqui
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-view-product',
  templateUrl: './view-product.page.html',
  styleUrls: ['./view-product.page.scss'],
  standalone: true,
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton,
    IonChip, IonLabel, IonSpinner, IonButton,
    IonFooter, // <--- 2. Adicionado na lista de componentes
    CommonModule
  ]
})
export class ViewProductPage implements OnInit {
  produto: any = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService,
    private carrinhoService: CarrinhoService,
    private toastController: ToastController
  ) { }

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.apiService.getProduto(id).subscribe({
        next: (res: any) => this.produto = res,
        error: (err: any) => console.error(err)
      });
    }
  }

  async adicionarAoCarrinho() {
    this.carrinhoService.adicionarItem(this.produto);
    
    const toast = await this.toastController.create({
      message: 'Produto adicionado ao carrinho! 🛒',
      duration: 2000,
      color: 'success',
      position: 'bottom'
    });
    toast.present();
  }
}