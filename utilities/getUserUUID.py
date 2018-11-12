def Num2UUID(num):
    user_map = dict()

    # Hackathon users
    user_map[1] = 'FDAE4FB1-FC87-462C-99F8-8BBED7F1FA6D'
    user_map[2] = '853B241E-1B76-426A-A37D-2A9B002D27AF'
    user_map[3] = '4C558948-80F1-4A9A-97FF-88D40BBF75FC'
    user_map[4] = 'B83930E1-D6A5-4BCB-B9FB-1F52D11AD5E2'
    user_map[5] = 'DB2D01C4-E406-4193-8DAE-C502C91EA3EA'
    user_map[6] = 'AB7C9B9C-11C1-48A8-B0FC-E9F1608BC4DA'
    user_map[7] = '58688E6C-5882-453A-8D64-8A8B43D3B477'
    user_map[8] = 'D0551550-AF70-4E83-B17D-31517ABD9905'
    user_map[9] = '38D7C8B2-9F07-40A4-9177-86BBA85C90AD'
    user_map[10] = '14C5AE77-282A-4172-A9B4-EB2AE28DC9CB'
    user_map[11] = '127931DA-D473-48C5-B622-500C61B5C149'
    user_map[12] = '93E172F5-3499-402B-9D8C-C07237CE7F6A'

    return user_map[num]

def Num2Partition(num):
    partition_map = dict()

    # Hackathon users
    partition_map[1] = 0
    partition_map[2] = 1
    partition_map[3] = 2
    partition_map[4] = 3
    partition_map[5] = 4
    partition_map[6] = 5
    partition_map[7] = 6
    partition_map[8] = 7
    partition_map[9] = 8
    partition_map[10] = 9
    partition_map[11] = 10
    partition_map[12] = 11

    return partition_map[num]
