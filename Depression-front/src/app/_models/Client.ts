export interface Client {
  person: Person,  
  email: string;
  comment: string;  
}

export interface Person {
  id: number,
  name: string,
  surname: string,
  patronymic: string,
  dateOfBirth: string
}
  