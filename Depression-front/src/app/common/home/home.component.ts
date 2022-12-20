import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl} from '@angular/forms';
import {ScoringService} from "../../_services";
import {formatDate} from "@angular/common";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  form: FormGroup;
  depressed: number;
  nonDepressed: number;
  result: boolean = null;
  formError: boolean = false;
  formMsg:string = "";


  /* Form's validation messages */
  validation_messages =
  {
    'text':
    [
      { type: 'required', message: 'Нужен текст' }
    ],
    'date_of_birth': [
      { type: 'required', message: 'Пожалуйста, укажите дату' },
    ],
    'gender' :[
      { type: 'required', message: 'Укажите пол'}
    ]
  };

  constructor(private fb: FormBuilder,
              private service: ScoringService) { }

  ngOnInit() {
    this.createForms();
  }


  get formControlId() { return this.form.get('text'); }
  get formControlDate() { return this.form.get('date_of_birth'); }

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
        date_of_birth: ['', Validators.required],
        gender: ['M']
      }
    )
  }

  onSubmit(event: any)
  {
    var body = {text:event.text, date_of_birth: formatDate(event.date_of_birth,"yyyy-MM-dd","en-EN"),sex: event.gender};

    console.log(body);
    this.service.score(body).subscribe(
      (response:any) => {
        this.result = response.depression_detection_result == "DEPRESSIVE";
        console.log(response)
        this.formControlId.reset();
        this.formControlId.setValidators([
          Validators.required
        ])
        this.formControlId.updateValueAndValidity();
        this.formControlId.markAsPristine();
        this.formControlId.markAsUntouched();
        this.depressed = Math.round(response.depressive_text_amount*100);
        this.nonDepressed = Math.round(response.non_depressive_text_amount*100);
        //console.log(Math.round(this.depressed*100)+" "+Math.round(this.nonDepressed*100));
        setTimeout
        (
          ()=> document.getElementById("pie").style.background = "radial-gradient(circle closest-side,transparent 66%,white 0),conic-gradient(#4e79a7 0,#4e79a7 "+this.depressed+"%,#f28e2c 0,#f28e2c "+this.nonDepressed+"%)",
        1000
        );

        this.formError = false;
        this.formMsg = "Запрос успешно отправлен";

        setTimeout
        (
          () => this.formMsg = "",
          5000
        );

      },
      error => {
        this.result = null;
        this.formError = true;
        this.formMsg = "Произошла ошибка, повторите попытку позже";

        setTimeout
        (
          () =>
          {
            this.formMsg = "";
            this.formError = false;
          },
          5000
        );
      }
    )
  }


}
