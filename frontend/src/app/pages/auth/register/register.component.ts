import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { AbstractControl, ReactiveFormsModule, Validators, FormBuilder, FormGroup, ValidationErrors } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../services/auth.service';

type RegisterDTO = { full_name: string; email: string; password: string };

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrls: ['./register.scss'],
})
export class Register {
  loading = false;
  errorMsg = '';
  form!: FormGroup; // la inicializamos en el constructor

  constructor(private fb: FormBuilder, private auth: AuthService, private router: Router) {
    // 👇 usar nonNullable para evitar string|null
    this.form = this.fb.nonNullable.group({
      full_name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });
  }

  // Validador asíncrono que consulta al backend
  private emailTakenValidator() {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      const value = (control.value ?? '').toString().trim();
      if (!value || control.invalid) return of(null); 
      return this.auth.checkEmail(value).pipe(
        map(res => (res.available ? null : { emailTaken: true })),
        catchError(() => of(null))
      );
    };
  }

  // arriba, junto a loading/errorMsg:
successMsg = '';  // 👈 nuevo

  submit() {
    if (this.form.invalid) return;

    const dto: RegisterDTO = this.form.getRawValue();

    this.loading = true;
    this.errorMsg = '';
    this.successMsg = ''; // limpiamos

    this.auth.register(dto).subscribe({
      next: () => {
        this.loading = false;
        // 👇 MOSTRAR CARTEL EN LA MISMA PANTALLA
        this.successMsg = '✅ Te enviamos un correo para confirmar tu cuenta. Revisá tu bandeja (y SPAM).';
        this.form.reset();

        // Si querés redirigir al login después de unos segundos, descomentá:
        // setTimeout(() => this.router.navigate(['/auth/login'], { queryParams: { registered: 1 } }), 2000);
      },
      error: (err) => {
        this.loading = false;
        this.errorMsg = err?.error?.detail || 'Error al registrar usuario';
      },
    });
  }
}