import { Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  // Rota inicial
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full',
  },
  
  // Rotas Públicas
  {
    path: 'login',
    loadComponent: () => import('./login/login.page').then( m => m.LoginPage)
  },
  {
    path: 'registro',
    loadComponent: () => import('./registro/registro.page').then( m => m.RegistroPage)
  },

  // --- ROTAS PROTEGIDAS (Só entra com Login) ---
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
    canActivate: [AuthGuard]
  },
  {
    path: 'view-product/:id',
    loadComponent: () => import('./view-product/view-product.page').then( m => m.ViewProductPage),
    canActivate: [AuthGuard]
  },
  {
    path: 'carrinho',
    loadComponent: () => import('./carrinho/carrinho.page').then( m => m.CarrinhoPage),
    canActivate: [AuthGuard]
  },
  {
    path: 'anunciar',
    loadComponent: () => import('./anunciar/anunciar.page').then( m => m.AnunciarPage),
    canActivate: [AuthGuard]
  },
  {
    path: 'meus-anuncios',
    loadComponent: () => import('./meus-anuncios/meus-anuncios.page').then( m => m.MeusAnunciosPage),
    canActivate: [AuthGuard]
  },
  // ESTA É A ROTA QUE FALTAVA:
  {
    path: 'editar-anuncio/:id',
    loadComponent: () => import('./editar-anuncio/editar-anuncio.page').then( m => m.EditarAnuncioPage),
    canActivate: [AuthGuard]
  },
  // ---------------------------------------------

  // Rota Coringa (Sempre a ÚLTIMA da lista)
  {
    path: '**',
    redirectTo: 'login',
    pathMatch: 'full',
  },
];