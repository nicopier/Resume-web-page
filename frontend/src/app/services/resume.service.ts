import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { ResumeItem } from '../models/resume.models';

// ==== Tipos del JSON completo ====

// Paso 1
export interface InformacionPersonal {
  locale: string;
  full_name: string;
  email: string;
  phone?: string;
  location?: string;
  birth_date?: string; // YYYY-MM-DD
}

// Paso 2
export interface Introduccion {
  about: string;
}

// Paso 3
export interface Estudio {
  school: string;
  degree: string;
  start?: string;
  end?: string;
  still: boolean;
}

// Paso 4
export interface Experiencia {
  company: string;
  role: string;
  start?: string;
  end?: string;
  current: boolean;
  description: string;
}

// Paso 5
export interface Skill {
  name: string;
  level: string; // "Básico" | "Intermedio" | "Avanzado"
}

// Respuesta completa del backend (incluye data)
export interface ResumeDocOut {
  id: number;
  locale: string;
  version: number;
  is_current: boolean;
  data: {
    informacion_personal: InformacionPersonal;
    introduccion: Introduccion;
    estudios: Estudio[];
    experiencia: Experiencia[];
    skills: Skill[];
  };
}

// Payload completo
export interface ResumePayload {
  data: {
    informacion_personal: InformacionPersonal;
    introduccion: Introduccion;
    estudios: Estudio[];
    experiencia: Experiencia[];
    skills: Skill[];
  };
}

@Injectable({ providedIn: 'root' })
export class ResumeService {
  private http = inject(HttpClient);
  private api = environment.apiUrl;

  // 👉 Método único: acepta el JSON completo
  create(payload: ResumePayload) {
    return this.http.post(`${this.api}/resume`, payload);
  }

  // NUEVOS MÉTODOS
  listMine() {
    return this.http.get<ResumeItem[]>(`${this.api}/resume/me`);
  }

  getById(id: number) {
    return this.http.get<ResumeDocOut>(`${this.api}/resume/${id}`);
  }

  delete(id: number) {
    // DELETE /resume/{id}
    return this.http.delete<void>(`${this.api}/resume/${id}`);
  }

}
