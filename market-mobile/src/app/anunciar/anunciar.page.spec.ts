import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AnunciarPage } from './anunciar.page';

describe('AnunciarPage', () => {
  let component: AnunciarPage;
  let fixture: ComponentFixture<AnunciarPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(AnunciarPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
