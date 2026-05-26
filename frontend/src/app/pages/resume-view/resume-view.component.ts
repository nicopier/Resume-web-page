import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ResumeService, ResumeDocOut } from '../../services/resume.service';

@Component({
  selector: 'app-resume-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './resume-view.component.html',
  styleUrls: ['./resume-view.component.scss'],
})
export class ResumeViewComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private svc = inject(ResumeService);

  doc = signal<ResumeDocOut | null>(null);
  loading = signal(true);
  error = signal<string | null>(null);

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.svc.getById(id).subscribe({
      next: (res) => {
        this.doc.set(res);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('No se pudo cargar el resume.');
        this.loading.set(false);
      },
    });
  }

  print(): void {
    window.print();
  }

  back(): void {
    this.router.navigateByUrl('/resume');
  }
}
