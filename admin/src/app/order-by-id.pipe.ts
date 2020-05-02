import { Pipe, PipeTransform } from '@angular/core';

interface HasID {
  _id: any;
}

@Pipe({
  name: 'orderByID',
  pure: false
})
export class OrderByIDPipe implements PipeTransform {

  transform(arrayIn: readonly any[], ascending?: boolean) {
    const sortFunc = (ascending ?
      (a: HasID, b: HasID) => { return a._id > b._id ? 1 : -1; }:
      (a: HasID, b: HasID) => { return a._id < b._id ? 1 : -1; });
    return Array.from(arrayIn).sort(sortFunc);
  }
}
