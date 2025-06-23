import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import App from './App';

// mock fetch used in App
global.fetch = vi.fn(() =>
  Promise.resolve({ json: () => Promise.resolve({}) })
);

describe('App', () => {
  it('renders title', () => {
    render(<App />);
    expect(screen.getByText(/The Corporation/i)).toBeTruthy();
  });
});
