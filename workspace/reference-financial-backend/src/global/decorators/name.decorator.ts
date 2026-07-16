import {
  registerDecorator,
  ValidationOptions,
  ValidatorConstraint,
  ValidatorConstraintInterface,
} from 'class-validator';

@ValidatorConstraint({ async: false })
export class IsRealNameConstraint implements ValidatorConstraintInterface {
  validate(name: string) {
    if (typeof name !== 'string') return false;
    name = name.trim();

    // Allow letters, accents, spaces, apostrophes, hyphens
    const pattern = /^[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,70}$/;
    if (!pattern.test(name)) return false;

    // Split into name parts
    const parts = name.split(/\s+/);
    if (parts.length > 5) return false; // too many words = weird

    // Each word must start with a letter
    for (const part of parts) {
      if (!/^[A-Za-zÀ-ÖØ-öø-ÿ]/.test(part)) return false;
    }

    // Count vowels / consonants
    const vowels = (name.match(/[aeiouAEIOUÀ-ÖØ-öø-ÿ]/g) || []).length;
    const consonants = (name.match(/[bcdfghjklmnpqrstvwxyz]/gi) || []).length;

    if (vowels === 0) return false; // no real name has zero vowels

    // Ratio check (rejects random strings)
    if (vowels / Math.max(consonants, 1) < 0.2) return false;

    // Reject long consonant clusters (random-like)
    if (/[bcdfghjklmnpqrstvwxyz]{5,}/i.test(name)) return false;

    // Reject excessive uppercase (random patterns)
    const uppercaseCount = (name.match(/[A-Z]/g) || []).length;
    if (uppercaseCount > parts.length * 2) return false; // sensible limit

    // Reject alternating case patterns (a common random string artifact)
    if (/([A-Z][a-z]){3,}|([a-z][A-Z]){3,}/.test(name)) return false;

    return true;
  }

  defaultMessage() {
    return 'Please enter a real full name.';
  }
}

export function IsRealName(options?: ValidationOptions) {
  return function (object: any, propertyName: string) {
    registerDecorator({
      target: object.constructor,
      propertyName,
      options,
      validator: IsRealNameConstraint,
    });
  };
}
