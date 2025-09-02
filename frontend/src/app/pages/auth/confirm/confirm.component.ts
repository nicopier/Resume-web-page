import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

@Component({
  standalone: true,
  selector: 'app-confirm',
  imports: [CommonModule],
  templateUrl: './confirm.component.html',
  styleUrls: ['./confirm.scss'],
})
export class ConfirmComponent {
  private route = inject(ActivatedRoute);
  private http = inject(HttpClient);

  token = '';
  status: 'idle' | 'verifying' | 'success' | 'error' = 'idle';
  message = '';
  userId = '';

  ngOnInit() {
    this.token = this.route.snapshot.queryParamMap.get('token') || '';
    if (!this.token) {
      this.status = 'error';
      this.message = 'Falta el token en la URL.';
      return;
    }

    this.status = 'verifying';
    const url = `${environment.apiUrl}/auth/confirm?token=${encodeURIComponent(this.token)}`;

    this.http.get<{ ok: boolean; user_id: string; already_verified?: boolean }>(url)
      .subscribe({
        next: (res) => {
          if (res?.ok) {
            this.userId = res.user_id;
            this.status = 'success';
            this.message = res.already_verified
              ? 'Tu cuenta ya estaba verificada.'
              : '¡Tu cuenta fue verificada con éxito!';
          } else {
            this.status = 'error';
            this.message = 'No se pudo verificar la cuenta.';
          }
        },
        error: (err) => {
          this.status = 'error';
          this.message = err?.error?.detail || 'Token inválido o vencido.';
        }
      });
  }

  goLogin() {
    // redirigí como prefieras; si usás routerLink en el template no hace falta
    window.location.href = '/auth/login';
  }
}
