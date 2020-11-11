import { Component, OnInit } from '@angular/core';
import { Card } from '../card';

@Component({
  selector: 'app-deck',
  templateUrl: './deck.component.html',
})
export class DeckComponent implements OnInit {
  card: Card = {
    id: 1,
    title: "Mario",
    description: "it's the mario",
    secret_description: "",
    order: "1",
    order_display: "1",
  }

  constructor() { }

  ngOnInit() {
  }
}
