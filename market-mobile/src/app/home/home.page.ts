import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Router, RouterLink } from '@angular/router';


// 1. Imports de Navegação e Ícones
import { NavController } from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { logOutOutline, cartOutline, add, gameController } from 'ionicons/icons';

// 2. Importando TODOS os componentes visuais
import { 
  IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonCard, 
  IonCardHeader, IonCardSubtitle, IonCardTitle, IonCardContent,
  IonButton, IonButtons, IonChip, IonLabel, IonIcon,
  IonSearchbar,  // <--- NOVO
  IonFab,        // <--- NOVO
  IonFabButton   // <--- NOVO
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: true,
  imports: [
    IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonCard, 
    IonCardHeader, IonCardSubtitle, IonCardTitle, IonCardContent,
    IonButton, IonButtons, IonChip, IonLabel, IonIcon,
    IonSearchbar,  // <--- Adicionado na lista
    IonFab,        // <--- Adicionado na lista
    IonFabButton,  // <--- Adicionado na lista
    CommonModule, HttpClientModule, RouterLink
  ],
})
export class HomePage implements OnInit {
  items: any[] = [];
  categoriaSelecionada = ''; 
  termoBusca = ''; // Variável para guardar o texto da busca

  filtros = [
    { label: 'Todos', valor: '' },
    { label: 'Jogos', valor: 'JOGO' },
    { label: 'Consoles', valor: 'CONSOLE' },
    { label: 'Acessórios', valor: 'ACESSORIO' }
  ];

  constructor(
    private apiService: ApiService, 
    private router: Router,
    private navCtrl: NavController 
  ) {
    // Registrando os ícones
    addIcons({ logOutOutline, cartOutline, add, gameController });
  }

  ngOnInit() {
    this.carregarDados();
  }

  // Função atualizada para aceitar Categoria E Busca
  carregarDados(categoria: string = '', busca: string = '') {
    this.categoriaSelecionada = categoria;
    
    // Agora passamos os dois parâmetros para o serviço
    this.apiService.getDados(categoria, busca).subscribe({
      next: (res: any) => this.items = res,
      error: (err: any) => console.error('Erro:', err)
    });
  }

  // Função chamada quando você digita na barra de pesquisa
  buscar(event: any) {
    this.termoBusca = event.detail.value;
    // Recarrega mantendo a categoria atual, mas com o texto novo
    this.carregarDados(this.categoriaSelecionada, this.termoBusca); 
  }

  abrirDetalhes(produto: any) {
    this.router.navigate(['/view-product', produto.id]);
  }

  logout() {
    localStorage.removeItem('token');
    this.navCtrl.navigateRoot('/login', { animationDirection: 'back' });
  }
}