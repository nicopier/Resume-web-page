import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ResumeService } from '../../services//resume.service'; // ajusta la ruta real
import { ResumeItem } from '../../models/resume.models';

@Component({
  selector: 'app-resume',
  standalone: true,
  imports: [CommonModule, RouterLink, DatePipe, MatTableModule, MatButtonModule, MatIconModule, MatSnackBarModule],
  templateUrl: './resume.component.html',  // ← singular
  styleUrls: ['./resume.scss']    // o styleUrl si usás 1 solo
})

export class ResumeComponent implements OnInit {
  private snack = inject(MatSnackBar);
  private router = inject(Router);
  private svc = inject(ResumeService);

  loading = signal<boolean>(false);
  data = signal<ResumeItem[]>([]);
  displayedColumns =  ['id', 'updated', 'actions'];

  ngOnInit(): void {
    this.cargar();
  }

  

  cargar(): void {
    this.loading.set(true);
    this.svc.listMine().subscribe({
      next: (res) => this.data.set(res ?? []),
      error: () => this.snack.open('No se pudieron cargar tus resumes', 'Cerrar', { duration: 3000 }),
      complete: () => this.loading.set(false),
    });
  }

  editar(id: number): void {
    // Reutilizamos tu pantalla de creación para edición con query param ?id=
    this.router.navigate(['/crear-resume'], { queryParams: { id } });
  }

  descargar(id: number): void {
    // Placeholder por ahora
    this.snack.open('Descarga: disponible próximamente', 'Ok', { duration: 2500 });
    // Cuando implementes el backend de descarga, acá iría:
    // this.svc.download(id).subscribe(...)
  }

  eliminar(id: number): void {
    const ok = confirm('¿Eliminar este resume? Esta acción no se puede deshacer.');
    if (!ok) return;

    this.svc.delete(id).subscribe({
      next: () => {
        this.snack.open('Resume eliminado', 'Cerrar', { duration: 2000 });
        this.cargar();
      },
      error: () => this.snack.open('No se pudo eliminar', 'Cerrar', { duration: 3000 }),
    });
  }
}
