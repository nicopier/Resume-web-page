import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormArray, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-step-skills',
  standalone: true,
  imports: [
    CommonModule, ReactiveFormsModule,
    MatFormFieldModule, MatInputModule, MatSelectModule, MatButtonModule
  ],
  templateUrl: './step-skills.component.html'
})
export class StepSkillsComponent {
  @Input({ required: true }) array!: FormArray<FormGroup>;
  @Output() add = new EventEmitter<void>();
  @Output() remove = new EventEmitter<number>();

  levels = ['Básico', 'Intermedio', 'Avanzado'];
}
