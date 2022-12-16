import {Client} from './Client'

export interface Order {
  id: number,
  comment:string,
  client: Client,
  specialization: Spec,
  modifications: Mod[]
}

export interface Spec {
name: string, 
}

export interface Mod {
name: string,
price: number,
currency: string
}

