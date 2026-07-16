import { registerDecorator, ValidationOptions } from 'class-validator';

export function IsEmptyHoneypot(options?: ValidationOptions) {
  return function (object: any, propertyName: string) {
    registerDecorator({
      target: object.constructor,
      propertyName,
      options,
      validator: {
        validate(value: string) {
          return !value; // must be empty
        },
        defaultMessage() {
          return 'Bot detected.';
        },
      },
    });
  };
}
