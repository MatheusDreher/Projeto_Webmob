import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // URL Base do servidor (sem /produtos no final)
  private baseUrl = 'http://127.0.0.1:8000/api'; 

  constructor(private http: HttpClient) { }

  // --- AUTENTICAÇÃO ---
  login(dados: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/login/`, dados);
  }

  cadastrar(dados: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/cadastro/`, dados);
  }

  // --- PRODUTOS ---
  // Busca com filtros opcionais
  getDados(categoria: string = '', busca: string = ''): Observable<any> {
    let url = `${this.baseUrl}/produtos/?dummy=1`;
    if (categoria) url += `&categoria=${categoria}`;
    if (busca) url += `&busca=${busca}`;
    return this.http.get(url);
  }

  getProduto(id: any): Observable<any> {
    return this.http.get(`${this.baseUrl}/produtos/${id}/`);
  }

  // --- MEUS ANÚNCIOS (Protegidos) ---
  getMeusAnuncios(): Observable<any> {
    return this.http.get(`${this.baseUrl}/meus-anuncios/`, { headers: this.getHeaders() });
  }

  criarProduto(formData: FormData): Observable<any> {
    return this.http.post(`${this.baseUrl}/anunciar/`, formData, { headers: this.getHeaders() });
  }

  atualizarProduto(id: any, formData: FormData): Observable<any> {
    return this.http.post(`${this.baseUrl}/editar-anuncio/${id}/`, formData, { headers: this.getHeaders() });
  }

  deletarProduto(id: any): Observable<any> {
    return this.http.delete(`${this.baseUrl}/meus-anuncios/${id}/`, { headers: this.getHeaders() });
  }

  // Função auxiliar para pegar o token
  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  realizarCompra(listaIds: any[]): Observable<any> {
    const headers = this.getHeaders();
    // Envia um objeto JSON com a lista de IDs
    return this.http.post(`${this.baseUrl}/comprar/`, { ids: listaIds }, { headers });
  }
}