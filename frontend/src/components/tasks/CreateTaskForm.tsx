'use client';

import { useState } from 'react';
import Button from '../ui/Button';
import Input from '../ui/Input';
import ErrorMessage from '../ui/ErrorMessage';
import { createTask } from '@/lib/api';
import type { Task } from '@/lib/types';

interface CreateTaskFormProps {
  onTaskCreated: (task: Task) => void;
}

export default function CreateTaskForm({ onTaskCreated }: CreateTaskFormProps) {
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      setError('Task title cannot be empty');
      return;
    }

    setIsLoading(true);

    try {
      const newTask = await createTask(trimmedTitle);
      setTitle('');
      onTaskCreated(newTask);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create task. Please try again.';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <ErrorMessage message={error} />

      <div className="flex gap-3">
        <div className="flex-1">
          <Input
            type="text"
            name="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            disabled={isLoading}
          />
        </div>
        <Button
          type="submit"
          isLoading={isLoading}
        >
          Add Task
        </Button>
      </div>
    </form>
  );
}
