// src/app/core/guards/auth.guard.ts
import { CanMatchFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthTokenService } from '../auth-token.service';

export const authGuard: CanMatchFn = () => {
  const token = inject(AuthTokenService);
  const router = inject(Router);
  return token.isLoggedIn() ? true : router.parseUrl('/auth/login');
};


