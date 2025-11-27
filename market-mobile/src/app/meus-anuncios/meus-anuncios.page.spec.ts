import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MeusAnunciosPage } from './meus-anuncios.page';

describe('MeusAnunciosPage', () => {
  let component: MeusAnunciosPage;
  let fixture: ComponentFixture<MeusAnunciosPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(MeusAnunciosPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
