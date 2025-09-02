import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router'; // 👈 importa RouterOutlet

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],                      // 👈 agregalo acá
  templateUrl: './app.html',
})
export class App {}