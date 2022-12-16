import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl} from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  form: FormGroup;  

  /* Form's validation messages */
  validation_messages =
  {
    'text':
    [
      { type: 'required', message: 'Нужен текст' }      
    ],
    'date': [
      { type: 'required', message: 'Пожалуйста, укажите дату' },
    ],
    'gender' :[
      { type: 'required', message: 'Укажите пол'}
    ]
  };

  constructor(private fb: FormBuilder) { }  

  ngOnInit() {

    this.createForms();
  }


  get formControlId() { return this.form.get('text'); }  
  get formControlDate() { return this.form.get('date'); }

  createForms()
  {
    this.form = this.fb.group(
      {
        text: new FormControl('',
          Validators.compose(
            [
              Validators.required              
            ]
          )
        ),
        date: ['', Validators.required],
        gender: ['male']
      }
    )
  }  
  
  onSubmit(event: any)
  {
    console.log(event);
  }


}
