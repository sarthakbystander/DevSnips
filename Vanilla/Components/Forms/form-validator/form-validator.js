/**
 * Snippet Name: Form Validator
 * Description: Validates required, email, and minimum length rules.
 * Author: DevSnips Contributors
 * Usage Example: const errors = validateForm(values, rules);
 */

const validators = {
  required: (value) => value.trim().length > 0,
  email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
  minLength: (value, length) => value.trim().length >= Number(length)
};

const validateForm = (values, rules) => Object.entries(rules).reduce((errors, [field, fieldRules]) => {
  const value = String(values[field] ?? '');
  const failedRule = fieldRules.find(({ rule, param }) => !validators[rule](value, param));

  if (failedRule) {
    errors[field] = failedRule.message;
  }

  return errors;
}, {});

export default validateForm;
