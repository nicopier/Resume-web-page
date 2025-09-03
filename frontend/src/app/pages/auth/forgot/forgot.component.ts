import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-forgot',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './forgot.component.html',
  styleUrls: ['./forgot.scss'],
})
export class ForgotComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);

  loading = false;
  sent = false;

  // ⬇⬇ claves para rate limit
  rateLimited = false;
  rateLimitMin = 0;

  errorMsg = '';

  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
  });
  get f() { return this.form.controls; }

  submit() {
    // limpiar todo antes de llamar
    this.errorMsg = '';
    this.sent = false;
    this.rateLimited = false;
    this.rateLimitMin = 0;

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading = true;
    const email = this.form.value.email as string;

    this.auth.forgotPassword({ email }).subscribe({
      next: () => {
        this.loading = false;
        this.sent = true; // 204 OK
      },
      error: (err) => {
        this.loading = false;

        // payload puede venir como {detail:{...}} o plano
        const payload = err?.error ?? {};
        const detail  = (payload && typeof payload.detail === 'object') ? payload.detail : null;

        const code    = (detail?.code ?? payload?.code) as string | undefined;
        const minutes = Number(detail?.minutes ?? payload?.minutes ?? NaN);

        if (err?.status === 429 && code === 'FORGOT_RATE_LIMIT') {
          this.rateLimited  = true;
          this.rateLimitMin = Number.isFinite(minutes) ? minutes : 5;
          this.sent = false;
          this.errorMsg = '';   // evita [object Object]
          return;
        }

        // fallback legible
        if (typeof payload === 'string') this.errorMsg = payload;
        else if (typeof payload?.detail === 'string') this.errorMsg = payload.detail;
        else this.errorMsg = 'No se pudo enviar el enlace. Intentá nuevamente.';
      }
,
    });
  }
}
