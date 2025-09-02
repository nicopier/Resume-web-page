import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormArray, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatButtonModule } from '@angular/material/button';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';

@Component({
  selector: 'app-step-education',
  standalone: true,
  imports: [
    CommonModule, ReactiveFormsModule,
    MatFormFieldModule, MatInputModule, MatCheckboxModule,
    MatButtonModule, MatDatepickerModule, MatNativeDateModule
  ],
  templateUrl: './step-education.component.html'
})
export class StepEducationComponent {
  @Input({ required: true }) array!: FormArray<FormGroup>;
  @Output() add = new EventEmitter<void>();
  @Output() remove = new EventEmitter<number>();
}
