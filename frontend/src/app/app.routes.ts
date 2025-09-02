import { Routes } from '@angular/router';
import { ShellComponent } from './layout/shell/shell.component';
import { authGuard } from './core/guards/auth.guard';
import { guestGuard } from './core/guards/guest.guard';
import { HomeComponent } from './pages/home/home.component';
import { ForgotComponent } from './pages/auth/forgot/forgot.component';
import { ConfirmComponent } from './pages/auth/confirm/confirm.component';

export const routes: Routes = [
  { path: 'forgot-password', component: ForgotComponent },
  { path: '', pathMatch: 'full', redirectTo: 'auth/login' },

  {
    path: 'auth',
    canMatch: [guestGuard],
    children: [
      { path: 'login',    loadComponent: () => import('./pages/auth/login/login.component').then(m => m.LoginComponent) },
      { path: 'register', loadComponent: () => import('./pages/auth/register/register.component').then(m => m.Register) },
      { path: 'forgot',   loadComponent: () => import('./pages/auth/forgot/forgot.component').then(m => m.ForgotComponent) },
      { path: 'confirm', loadComponent: () => import('./pages/auth/confirm/confirm.component').then(m => m.ConfirmComponent) },
      { path: '', pathMatch: 'full', redirectTo: 'login' },
      
    ],
  },

  {
  path: '',
  component: ShellComponent,
  canMatch: [authGuard],
  children: [
    { path: 'home', component: HomeComponent },

    // 👇 MÁS ESPECÍFICA PRIMERO
    {
      path: 'resume/new',
      loadComponent: () =>
        import('./pages/resume-create/resume-create.component')
          .then(m => m.ResumeCreateComponent),
    },

    // 👇 LUEGO la general
    {
      path: 'resume',
      loadComponent: () => import('./pages/resume/resume.component').then(m => m.ResumeComponent),
    },
  ],
},
  { path: '**', redirectTo: 'auth/login' },
  
];
