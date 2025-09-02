// src/app/core/auth-token.service.ts
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthTokenService {
  get token(): string | null {
    return localStorage.getItem('access_token');
  }

  isLoggedIn(): boolean {
    const t = this.token;
    if (!t) return false;

    // Debe tener forma header.payload.signature
    if (!/^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$/.test(t)) return false;

    // Chequeo de exp si existe
    try {
      const payload = JSON.parse(atob(t.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
      if (payload?.exp && Date.now() / 1000 >= payload.exp) return false; // expirado
    } catch {
      return false;
    }
    return true;
  }

  clear() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
  }
}
