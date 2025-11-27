import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private router: Router) {}

  canActivate(): boolean {
    // Verifica se existe o token salvo no celular
    const token = localStorage.getItem('token');

    if (token) {
      // Tem token? Acesso liberado!
      return true;
    } else {
      // Não tem token? Manda para o Login!
      this.router.navigate(['/login']);
      return false;
    }
  }
}