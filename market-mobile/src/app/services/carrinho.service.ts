import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CarrinhoService {
  
  private itens: any[] = [];

  constructor() { }

  
  adicionarItem(produto: any) {
    this.itens.push(produto);
  }

  
  removerItem(index: number) {
    this.itens.splice(index, 1);
  }

  
  getItens() {
    return this.itens;
  }

 
  getTotal() {
    return this.itens.reduce((total, item) => total + Number(item.preco), 0);
  }
  
  
  limparCarrinho() {
    this.itens = [];
  }
}