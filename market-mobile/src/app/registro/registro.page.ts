import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { ToastController } from '@ionic/angular/standalone';

@Component({
  selector: 'app-registro',
  templateUrl: './registro.page.html',
  standalone: true,
  imports: [CommonModule, FormsModule, IonicModule]
})
export class RegistroPage {
  novoUsuario = { username: '', email: '', password: '' };

  constructor(private api: ApiService, private router: Router, private toast: ToastController) {}

  registrar() {
    this.api.cadastrar(this.novoUsuario).subscribe({
      next: async () => {
        const t = await this.toast.create({ message: 'Conta criada! Faça login.', duration: 2000, color: 'success' });
        t.present();
        this.router.navigate(['/login']);
      },
      error: async () => {
        const t = await this.toast.create({ message: 'Erro ao criar conta. Tente outro nome.', duration: 2000, color: 'danger' });
        t.present();
      }
    });
  }
}