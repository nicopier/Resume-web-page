import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthTokenService } from '../../core/auth-token.service';

@Component({
  selector: 'app-shell',
  standalone: true,
  templateUrl: './shell.component.html',
  styleUrls: ['./shell.scss'],
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
})
export class ShellComponent {
  open = false;

  locales = [
    { code: 'es', label: 'ES', flag: '🇦🇷' },
    { code: 'en', label: 'EN', flag: '🇺🇸' },
    { code: 'pt', label: 'PT', flag: '🇧🇷' },
    { code: 'fr', label: 'FR', flag: '🇫🇷' },
    { code: 'zh', label: 'ZH', flag: '🇨🇳' },
  ];

  currentLocale: string;

  constructor(private router: Router, private auth: AuthTokenService) {
    const match = window.location.pathname.match(/^\/(es|en|pt|fr|zh)(\/|$)/);
    this.currentLocale = match ? match[1] : 'es';
  }

  switchLocale(code: string) {
    if (code === this.currentLocale) return;
    const rest = window.location.pathname.replace(/^\/(es|en|pt|fr|zh)(\/|$)/, '/');
    window.location.href = `/${code}${rest === '/' ? '' : rest}${window.location.search}`;
  }

  logout() {
    this.auth.clear();
    this.router.navigateByUrl('/auth/login');
  }
}
