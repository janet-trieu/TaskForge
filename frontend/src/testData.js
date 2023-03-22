const testData = {
    tasks: {
        'task-1': { id: 'task-1', content: 'Take out the garbage' },
        'task-2': { id: 'task-2', content: 'Watch my favorite show' },
        'task-3': { id: 'task-3', content: 'Charge my phone' },
        'task-4': { id: 'task-4', content: 'Cook dinner' },
        'task-5': { id: 'task-5', content: 'Take out the garbage 2' },
        'task-6': { id: 'task-6', content: 'Watch my favorite show 2' },
        'task-7': { id: 'task-7', content: 'Charge my phone 2' },
        'task-8': { id: 'task-8', content: 'Cook dinner 2' },
    },
    columns: {
        'column-1': {
            id: 'column-1',
            title: 'To do',
            taskIds: ['task-1', 'task-2', 'task-3', 'task-4'],
        },
        'column-2': {
            id: 'column-2',
            title: 'Two do',
            taskIds: ['task-5', 'task-6', 'task-7', 'task-8']
        }
    },
    // Facilitate reordering of the columns
    columnOrder: ['column-1', 'column-2']
}

export default testData;