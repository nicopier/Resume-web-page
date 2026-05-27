import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-locale-switcher',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="locale-switcher">
      <button
        *ngFor="let loc of locales"
        class="locale-btn"
        [class.active]="loc.code === currentLocale"
        type="button"
        (click)="switchLocale(loc.code)"
        [attr.title]="loc.label">
        {{ loc.flag }}
      </button>
    </div>
  `,
  styles: [`
    .locale-switcher { display: flex; gap: 2px; }
    .locale-btn {
      background: none;
      border: 1px solid transparent;
      border-radius: 4px;
      cursor: pointer;
      font-size: 1.15rem;
      line-height: 1;
      padding: 0.2rem 0.3rem;
      opacity: 0.5;
      transition: opacity 0.2s, border-color 0.2s;
    }
    .locale-btn:hover { opacity: 0.9; }
    .locale-btn.active { opacity: 1; border-color: rgba(255,255,255,0.25); }
  `]
})
export class LocaleSwitcherComponent {
  locales = [
    { code: 'es', label: 'ES', flag: '🇦🇷' },
    { code: 'en', label: 'EN', flag: '🇺🇸' },
    { code: 'pt', label: 'PT', flag: '🇧🇷' },
    { code: 'fr', label: 'FR', flag: '🇫🇷' },
    { code: 'zh', label: 'ZH', flag: '🇨🇳' },
  ];

  currentLocale: string;

  constructor() {
    const match = window.location.pathname.match(/^\/(es|en|pt|fr|zh)(\/|$)/);
    this.currentLocale = match ? match[1] : 'es';
  }

  switchLocale(code: string) {
    if (code === this.currentLocale) return;
    const rest = window.location.pathname.replace(/^\/(es|en|pt|fr|zh)(\/|$)/, '/');
    window.location.href = `/${code}${rest === '/' ? '' : rest}${window.location.search}`;
  }
}
