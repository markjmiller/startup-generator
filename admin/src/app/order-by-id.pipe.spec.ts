import { OrderByIDPipe } from './order-by-id.pipe';

const array = ['a1', '15', 'cd', '51'].map(x => { return {'_id': x}});

describe('OrderByIDPipe', () => {
  it('orders by ID ascending', () => {
    const pipe = new OrderByIDPipe();
    const result = pipe.transform(array, true);
    expect(result.map(x => x._id)).toEqual(['15', '51', 'a1', 'cd']);
  });
});

describe('OrderByIDPipe', () => {
  it('orders by ID descending', () => {
    const pipe = new OrderByIDPipe();
    const result = pipe.transform(array);
    expect(result.map(x => x._id)).toEqual(['cd', 'a1', '51', '15']);
  });
});
