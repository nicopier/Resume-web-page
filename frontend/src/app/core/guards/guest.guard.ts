// src/app/core/guards/guest.guard.ts
import { CanMatchFn, Router, UrlSegment, Route } from '@angular/router';
import { inject } from '@angular/core';
import { AuthTokenService } from '../auth-token.service';

export const guestGuard: CanMatchFn = (_: Route, __: UrlSegment[]) => {
  const token = inject(AuthTokenService);
  const router = inject(Router);
  if (!token.isLoggedIn()) return true;
  router.navigateByUrl('/home');
  return false;
};
