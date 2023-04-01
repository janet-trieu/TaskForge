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
        'task-9': { id: 'task-9', content: 'Take out the garbage 3' },
        'task-10': { id: 'task-10', content: 'Watch my favorite show 3' },
        'task-11': { id: 'task-11', content: 'Charge my phone 3' },
        'task-12': { id: 'task-12', content: 'Cook dinner 3' },
        'task-13': { id: 'task-13', content: 'Take out the garbage 4' },
        'task-14': { id: 'task-14', content: 'Watch my favorite show 4' },
        'task-15': { id: 'task-15', content: 'Charge my phone 4' },
        'task-16': { id: 'task-16', content: 'Cook dinner 4' },
    },
    columns: {
        'column-1': {
            id: 'column-1',
            title: 'TO DO',
            taskIds: ['task-1', 'task-2', 'task-3', 'task-4'],
        },
        'column-2': {
            id: 'column-2',
            title: 'IN PROGRESS',
            taskIds: ['task-5', 'task-6', 'task-7', 'task-8']
        },
        'column-3': {
            id: 'column-3',
            title: 'NEEDS REVIEWING',
            taskIds: ['task-9', 'task-10', 'task-11', 'task-12']
        },
        'column-4': {
            id: 'column-4',
            title: 'COMPLETED',
            taskIds: ['task-13', 'task-14', 'task-15', 'task-16']
        }
    },
    // Facilitate reordering of the columns
    columnOrder: ['column-1', 'column-2', 'column-3', 'column-4']
}

export default testData;