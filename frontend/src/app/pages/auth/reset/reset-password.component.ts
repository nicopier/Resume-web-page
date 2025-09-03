import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../services/auth.service';

@Component({
  standalone: true,
  selector: 'app-reset-password',
  imports: [CommonModule, ReactiveFormsModule,RouterLink],
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.scss'],
})


export class ResetPasswordComponent {
  private fb = inject(FormBuilder);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private auth = inject(AuthService);

  token = this.route.snapshot.queryParamMap.get('token') || '';
  loading = false;
  successMsg = '';
  errorMsg = '';
  
  errorCode: string | null = null;

  // form con validador de coincidencia
  form = this.fb.group(
    {
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirm:  ['', [Validators.required]],
    },
    { validators: this.match('password', 'confirm') }
  );

  get f() { return this.form.controls; }

  private match(pw: string, cf: string) {
    return (group: any) => {
      const p = group.get(pw)?.value;
      const c = group.get(cf)?.value;
      return p && c && p === c ? null : { mismatch: true };
    };
  }
success = false;   // <- en lugar de successMsg: string

submit() {
  this.errorMsg = '';
  this.success = false;

  if (!this.token) {
    this.errorMsg = 'Token inválido o ausente.';
    return;
  }
  if (this.form.invalid) {
    this.form.markAllAsTouched();
    return;
  }

  this.loading = true;
  this.auth.resetPassword({
    token: this.token,
    new_password: this.form.value.password!,
  }).subscribe({
    next: () => {
      this.loading = false;
      this.success = true;                 // <- solo flag
      // opcional: auto-redirect después de 5s
      // setTimeout(() => this.router.navigate(['/auth/login']), 5000);
    },
    error: (err) => {
      this.loading = false;
      const e = err?.error;
      if (typeof e === 'string') this.errorMsg = e;
      else if (typeof e?.detail === 'string') this.errorMsg = e.detail;
      else this.errorMsg = 'No se pudo actualizar la contraseña.';
    },
  });
}
}
