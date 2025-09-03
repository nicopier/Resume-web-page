import { Routes } from '@angular/router';
import { ShellComponent } from './layout/shell/shell.component';
import { authGuard } from './core/guards/auth.guard';
import { guestGuard } from './core/guards/guest.guard';
import { HomeComponent } from './pages/home/home.component';

// ❌ No importes componentes standalone si los cargás lazy
// import { ForgotComponent } from './pages/auth/forgot/forgot.component';
// import { ConfirmComponent } from './pages/auth/confirm/confirm.component';

export const routes: Routes = [
  // 1) Rutas públicas que vienen desde email
  { path: 'reset-password', loadComponent: () => import('./pages/auth/reset/reset-password.component').then(m => m.ResetPasswordComponent) },
  { path: 'auth/confirm',  loadComponent: () => import('./pages/auth/confirm/confirm.component').then(m => m.ConfirmComponent) },

  // 2) Redirect raíz
  { path: '', pathMatch: 'full', redirectTo: 'auth/login' },

  // 3) Auth (solo para invitados)
  {
    path: 'auth',
    canMatch: [guestGuard],
    children: [
      { path: 'login',    loadComponent: () => import('./pages/auth/login/login.component').then(m => m.LoginComponent) },
      { path: 'register', loadComponent: () => import('./pages/auth/register/register.component').then(m => m.Register) },
      { path: 'forgot',   loadComponent: () => import('./pages/auth/forgot/forgot.component').then(m => m.ForgotComponent) },
      { path: '', pathMatch: 'full', redirectTo: 'login' },
    ],
  },

  // 4) App protegida
  {
    path: '',
    component: ShellComponent,
    canMatch: [authGuard],
    children: [
      { path: 'home', component: HomeComponent },

      { path: 'resume/new',
        loadComponent: () => import('./pages/resume-create/resume-create.component').then(m => m.ResumeCreateComponent),
      },
      { path: 'resume',
        loadComponent: () => import('./pages/resume/resume.component').then(m => m.ResumeComponent),
      },
    ],
  },

  // 5) 404
  { path: '**', redirectTo: 'auth/login' },
];
