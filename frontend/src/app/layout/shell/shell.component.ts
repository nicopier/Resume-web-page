import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthTokenService } from '../../core/auth-token.service'; // ajustá el path si cambia

@Component({
  selector: 'app-shell',
  standalone: true,
  templateUrl: './shell.component.html',
  styleUrls: ['./shell.scss'],
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
})
export class ShellComponent {
  open = false;

  constructor(private router: Router, private auth: AuthTokenService) {}

  logout() {
    this.auth.clear();
    this.router.navigateByUrl('/auth/login');
  }
}
