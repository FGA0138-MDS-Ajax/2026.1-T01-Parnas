import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { test } from 'vitest';
import Register from '/home/danielfilipe/2026.1-T01-Parnas/frontend/src/pages/Register/Register.jsx';

test('debug', async () => {
  render(<Register />);
  const d = document.querySelector('input[name="dataNascimento"]');
  fireEvent.change(d, { target: { value: '2099-01-01' } });
  console.log('VALUE APOS CHANGE:', d.value);
  await userEvent.click(screen.getByRole('button', { name: /finalizar registro/i }));
  screen.debug(document.querySelector('.register-form-content'));
});
