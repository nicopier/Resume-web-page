import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

type RegisterDTO = { full_name: string; email: string; password: string };
type ForgotPasswordDTO = { email: string };
type ResetPasswordDTO = { token: string; new_password: string };

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private api = environment.apiUrl;

  register(data: RegisterDTO) {
    return this.http.post(`${this.api}/auth/register`, data);
  }

  checkEmail(email: string) {
    return this.http.get<{ available: boolean }>(`${this.api}/auth/check-email`, {
      params: { email },
    });
  }
  // ============ NUEVOS MÉTODOS ============
  forgotPassword(data: ForgotPasswordDTO) {
    // backend responde 204 No Content
    return this.http.post<void>(`${this.api}/auth/forgot-password`, data);
  }

  resetPassword(data: ResetPasswordDTO) {
    // backend responde 204 No Content
    return this.http.post<void>(`${this.api}/auth/reset-password`, data);
  }

  resendConfirm(email: string) {
    return this.http.post<{ ok: boolean; message: string }>(
      `${this.api}/auth/resend-confirm`,
      { email }
    );
  }
}