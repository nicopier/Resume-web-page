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
  errorMsg = '';

  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
  });

  get f() { return this.form.controls; }

  submit() {
    this.errorMsg = '';
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading = true;
    const email = this.form.value.email as string;

    this.auth.forgotPassword({ email }).subscribe({
      next: () => {
        this.sent = true;       // mostramos mensaje “si existe, te mandamos el enlace”
        this.loading = false;
      },
      error: () => {
        // el backend devuelve 204 aunque el mail no exista; solo mostramos si falla la red/servidor
        this.errorMsg = 'No se pudo enviar el enlace. Intentá nuevamente.';
        this.loading = false;
      },
    });
  }
}
