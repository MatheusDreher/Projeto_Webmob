import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ToastController } from '@ionic/angular/standalone';

// 1. Imports Visuais
import { 
  IonContent, IonItem, IonLabel, IonInput, IonButton, IonIcon 
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { gameController, personOutline, lockClosedOutline } from 'ionicons/icons'; // <--- Novos ícones

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule, RouterLink,
    IonContent, IonItem, IonLabel, IonInput, IonButton, IonIcon
  ] 
})
export class LoginPage {
  usuario = { username: '', password: '' };

  constructor(
    private api: ApiService, 
    private router: Router,
    private toast: ToastController
  ) {
    // 2. Registrar ícones
    addIcons({ gameController, personOutline, lockClosedOutline });
  }

  fazerLogin() {
    if (!this.usuario.username || !this.usuario.password) {
      this.mostrarErro('Preencha usuário e senha');
      return;
    }

    this.api.login(this.usuario).subscribe({
      next: async (res: any) => {
        console.log('Login OK:', res);
        localStorage.setItem('token', res.access);
        this.router.navigate(['/home']);
      },
      error: async (err) => {
        this.mostrarErro('Usuário ou senha inválidos');
      }
    });
  }

  async mostrarErro(msg: string) {
    const t = await this.toast.create({ message: msg, duration: 2000, color: 'danger', position: 'top' });
    t.present();
  }
}