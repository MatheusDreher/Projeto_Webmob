import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EditarAnuncioPage } from './editar-anuncio.page';

describe('EditarAnuncioPage', () => {
  let component: EditarAnuncioPage;
  let fixture: ComponentFixture<EditarAnuncioPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(EditarAnuncioPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
