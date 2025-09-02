import { Component } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
interface LoginForm {
  email: FormControl<string>;
  password: FormControl<string>;
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.scss'],
})
export class LoginComponent {
  loading = false;
  errorMsg: string | null = null;

  // ▼ NUEVO estado
  unverified = false;
  resendLoading = false;
  cooldownUntil: number | null = null; // epoch ms para contador

  form: FormGroup<LoginForm>;

  constructor(private fb: FormBuilder, private router: Router) {
    this.form = this.fb.group<LoginForm>({
      email: this.fb.control('', { validators: [Validators.required, Validators.email], nonNullable: true }),
      password: this.fb.control('', { validators: [Validators.required, Validators.minLength(6)], nonNullable: true }),
    });
  }

  async onSubmit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.loading = true;
    this.errorMsg = null;
    this.unverified = false;

    try {
      const res = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.form.getRawValue()),
      });

      if (!res.ok) {
        // ⛔ detectar cuenta no verificada
        if (res.status === 403) {
          this.unverified = true;
          let detail = 'Cuenta no verificada.';
          try {
            const body = await res.json();
            if (body?.detail) detail = body.detail;
          } catch {}
          this.errorMsg = detail;
          return; // no tiramos error, mostramos cartel y botón
        }
        throw new Error((await res.text()) || 'Login failed');
      }

      const data = await res.json();
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('token_type', data.token_type || 'bearer');
      this.router.navigateByUrl('/home');
    } catch (err: any) {
      this.errorMsg = err?.message || 'Error desconocido';
    } finally {
      this.loading = false;
    }
  }

  // ▼ NUEVO: reenviar verificación
  async resend() {
    if (this.resendLoading) return;

    const email = this.form.controls.email.value?.trim();
    if (!email) {
      this.errorMsg = 'Ingresá tu email para reenviar la verificación.';
      return;
    }

    // cooldown en UI (el back también aplica 5 minutos)
    if (this.cooldownUntil && Date.now() < this.cooldownUntil) return;

    this.resendLoading = true;
    try {
      const res = await fetch('http://localhost:8000/auth/resend-confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      if (!res.ok) {
        if (res.status === 429) {
          // demasiadas solicitudes: mostramos msg y dejamos 1 min de cooldown visual
          let detail = 'Esperá unos minutos antes de volver a intentar.';
          try {
            const body = await res.json();
            if (body?.detail) detail = body.detail;
          } catch {}
          this.errorMsg = detail;
          this.cooldownUntil = Date.now() + 60 * 1000;
          return;
        }
        throw new Error((await res.text()) || 'No se pudo reenviar el correo.');
      }

      this.errorMsg = 'Te enviamos un nuevo correo de verificación.';
      // 5 minutos de cooldown visual
      this.cooldownUntil = Date.now() + 5 * 60 * 1000;
    } catch (err: any) {
      this.errorMsg = err?.message || 'No se pudo reenviar el correo.';
    } finally {
      this.resendLoading = false;
    }
  }

  // contador para el botón
  get cooldownSeconds(): number {
    if (!this.cooldownUntil) return 0;
    const s = Math.ceil((this.cooldownUntil - Date.now()) / 1000);
    return s > 0 ? s : 0;
  }
}
