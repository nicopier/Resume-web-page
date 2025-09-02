import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, Validators, ReactiveFormsModule, FormGroup, FormArray } from '@angular/forms';
import { MatStepperModule } from '@angular/material/stepper';
import { MatButtonModule }  from '@angular/material/button';

// hijos (steps)
import { StepPersonalComponent }   from './steps/step-personal.component';
import { StepIntroComponent }      from './steps/step-intro.component';
import { StepEducationComponent }  from './steps/step-education.component';
import { StepExperienceComponent } from './steps/step-experience.component';
import { StepSkillsComponent }     from './steps/step-skills.component';

// servicio
import { ResumeService } from '../../services/resume.service';

@Component({
  selector: 'app-resume-create',
  standalone: true,
  imports: [
    CommonModule, ReactiveFormsModule,
    MatStepperModule, MatButtonModule,
    StepPersonalComponent, StepIntroComponent, StepEducationComponent,
    StepExperienceComponent, StepSkillsComponent
  ],
  templateUrl: './resume-create.component.html',
  styleUrls: ['./resume-create.scss']
})
export class ResumeCreateComponent {
  stepLinear = true;
  locales = ['en', 'es', 'pt', 'fr', 'jp', 'in'];

  form!: FormGroup;
  loading = false;
  errorMsg = '';

  constructor(private fb: FormBuilder, private resume: ResumeService) {
    this.form = this.fb.group({
      // PASO 1 (en raíz, según tu schema)
      locale: ['en', Validators.required],
      full_name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      phone: [''],
      location: [''],
      birth_date: [''],

      // PASO 2
      intro: this.fb.group({
        about: ['', [Validators.required, Validators.minLength(40), Validators.maxLength(600)]],
      }),

      // PASO 3
      education: this.fb.array<FormGroup>([]),

      // PASO 4
      experience: this.fb.array<FormGroup>([]),

      // PASO 5
      skills: this.fb.array<FormGroup>([]),
    });

    // inicializa con 1 item en cada array
    this.addEducation();
    this.addExperience();
    this.addSkill();
  }

  // ===== Getters útiles para el template =====
  get introGroup(): FormGroup {
    return this.form.get('intro') as FormGroup;
  }
  educationArray(): FormArray<FormGroup> {
    return this.form.get('education') as FormArray<FormGroup>;
  }
  experienceArray(): FormArray<FormGroup> {
    return this.form.get('experience') as FormArray<FormGroup>;
  }
  skillsArray(): FormArray<FormGroup> {
    return this.form.get('skills') as FormArray<FormGroup>;
  }

  // ===== Helpers Education =====
  newEducation() {
    return this.fb.group({
      school: ['', Validators.required],
      degree: ['', Validators.required],
      start: [''],
      end: [''],
      still: [false],
    });
  }
  addEducation() { this.educationArray().push(this.newEducation()); }
  removeEducation(i: number) { this.educationArray().removeAt(i); }

  // ===== Helpers Experience =====
  newExperience() {
    return this.fb.group({
      company: ['', Validators.required],
      role: ['', Validators.required],
      start: [''],
      end: [''],
      current: [false],
      description: [''],
    });
  }
  addExperience() { this.experienceArray().push(this.newExperience()); }
  removeExperience(i: number) { this.experienceArray().removeAt(i); }

  // ===== Helpers Skills =====
  newSkill() {
    return this.fb.group({
      name: ['', Validators.required],
      level: ['Intermedio', Validators.required], // Básico / Intermedio / Avanzado
    });
  }
  addSkill() { this.skillsArray().push(this.newSkill()); }
  removeSkill(i: number) { this.skillsArray().removeAt(i); }
// ===== SUBMIT =====
submit() {
  if (this.form.invalid) return;

  const raw = this.form.value as any;

  const toISO = (d: any): string | undefined => {
    if (!d) return undefined;
    if (d instanceof Date) {
      const y = d.getFullYear();
      const m = String(d.getMonth() + 1).padStart(2, '0');
      const dd = String(d.getDate()).padStart(2, '0');
      return `${y}-${m}-${dd}`;
    }
    const m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(d);
    if (m) return `${m[3]}-${m[2]}-${m[1]}`;
    return d; // ya vendría yyyy-mm-dd
  };

  // JSON completo con todos los pasos
  const payload = {
    informacion_personal: {
      locale: raw.locale,
      full_name: raw.full_name,
      email: raw.email,
      phone: raw.phone || undefined,
      location: raw.location || undefined,
      birth_date: toISO(raw.birth_date),
    },
    introduccion: { about: raw.intro?.about ?? '' },
    estudios: (raw.education || []).map((e: any) => ({
      school: e.school,
      degree: e.degree,
      start: toISO(e.start),
      end: e.still ? undefined : toISO(e.end),
      still: !!e.still,
    })),
    experiencia: (raw.experience || []).map((e: any) => ({
      company: e.company,
      role: e.role,
      start: toISO(e.start),
      end: e.current ? undefined : toISO(e.end),
      current: !!e.current,
      description: e.description || '',
    })),
    skills: (raw.skills || []).map((s: any) => ({
      name: s.name,
      level: s.level,
    })),
  };

  this.loading = true;
  this.errorMsg = '';

  // ✅ siempre enviar con la key `data`
  this.resume.create({ data: payload }).subscribe({
    next: () => {
      this.loading = false;
      alert('CV guardado');
      console.log('JSON enviado al backend:', { data: payload });
    },
    error: (err: any) => {
      this.loading = false;
      const detail = err?.error?.detail;
      if (Array.isArray(detail)) {
        this.errorMsg = detail
          .map((e: any) => `${(e.loc || []).join('.')}: ${e.msg}`)
          .join('\n');
      } else {
        this.errorMsg =
          detail || err?.error?.message || err?.statusText || 'Error al guardar';
      }
      alert(this.errorMsg);
      console.error('Save error:', err);
    },
  });
}
// Marca el Paso 1 como completo solo con estos 3 campos válidos
isPersonalComplete(): boolean {
  const f = this.form;
  return !!(
    f.get('locale')?.valid &&
    f.get('full_name')?.valid &&
    f.get('email')?.valid
  );
}
}
