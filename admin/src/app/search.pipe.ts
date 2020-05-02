import { Pipe, PipeTransform } from '@angular/core';
import { Word } from './words.service';

@Pipe({
  name: 'search'
})
export class SearchPipe implements PipeTransform {

  private normalize(value: string) {
    return value.toLowerCase().replace(/the /g, '');
  }

  private search(findIn: string, value: string) {
    const regex = `${this.normalize(value)}`;
    var re = new RegExp(regex, "g");
    return this.normalize(findIn).match(re);
  }

  transform(value: readonly Word[], searchValue: string): readonly Word[] {
    if (!searchValue) { return value; }
    return Array.from(value).filter(x => this.search(x.word, searchValue));
  }
}
