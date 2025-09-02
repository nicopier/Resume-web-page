import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResumeCreate } from './resume-create';

describe('ResumeCreate', () => {
  let component: ResumeCreate;
  let fixture: ComponentFixture<ResumeCreate>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResumeCreate]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ResumeCreate);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
