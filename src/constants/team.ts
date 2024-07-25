const teamStatusMap: { [key: number]: string } = {
    0: '公开',
    1: '加密',
    2: '私有',
}

export const teamStatusEnum = (teamStatus: number): string => {
    return teamStatusMap[teamStatus]
}